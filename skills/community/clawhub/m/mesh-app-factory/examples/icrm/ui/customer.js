import {sta2icon} from '/assets/v3/components/workflow.js';
import {encodeExt,decodeExt} from '/assets/v3/settings/config.js';

export default {
inject:['service', 'tags', 'ibf'],
data() {return {
    id:this.$route.query.id,
    
    dtl:{}, //详情name,address,createAt,creator,taxid,flowid,status,business,comment
    orders:[], //id,createAt,price,skuName,creator
    contacts:[], //id,name,post,createAt
    touchlogs:[], //comment,createAt,creator
    shares:[],
    relationChart:null,
    curDate:'',//当前时间，用在分享界面
    
    prjInput:{},
    skuInput:{sku:{},num:'',price:'',suppliers:[]}, //用于创建订单界面
    newOrder:{price:0,nextSigners:[],ext:{},skus:[]},
    newContact:{name:'',sex:"0",level:0,phone:'',address:'',post:'',
                birthday:date2str(new Date()),ext:{}},
    newTl:{n:'',t:0,act:'',cid:0,cmt:''},
    newShare:{endT:'',to:[],power:"S"},
    
    page:{contact:1,curContact:1,touchlog:1,curTl:1,order:1,curOrder:1},
    visible:{editBase:false, order:false, contact:false, touchlog:false,
        newOrd:false, newContact:false, newTl:false,
        share:false, newShare:false, deliver:false, relation:false},
    visSegs:["name","taxid","address","business","creator","ordNum","createAt"] //控制哪些字段需要显示
}},
created(){
    this.curDate=date2str(new Date());
    var defaultVal={cmt:{n:this.tags.cmt,t:'s'}};
    var url="/api/proxy/gettemplate?name=customer";
    this.ibf.template('customer', url, defaultVal).then(tmpl=>{
        this.detail(tmpl);
    })
},
methods:{
detail(tmpl) {
    var url="/api/customer/detail?id="+this.id;
    request({method:"GET", url:url}, this.service.name).then(resp=>{
        if(resp.code != 0) {
            this.$refs.errMsg.showErr(resp.code, resp.info);
            return;
        }
        this.dtl=resp.data;//id,name,address,creator,createAt,ordNum,taxid,flowid,status,comment,power
        this.dtl.createAt=date2str(new Date(resp.data.createAt*60000));
        this.dtl.icon=sta2icon(this.dtl.status);
        this.dtl.ext=decodeExt(this.dtl.comment, tmpl);
    });
},
query_orders(pg) {
    var pgSize=this.service.N_SMPG;
    var offset=(parseInt(pg)-1)*pgSize;
    var url="/api/order/list?customer="+this.id+"&offset="+offset+"&num="+pgSize;
    request({method:"GET",url:url}, this.service.name).then(resp=>{
        if(resp.code!=0||resp.data.total==0) {
            return;
        }
        var orders=[];
        var dt=new Date();
        for(var o of resp.data.orders){
            dt.setTime(o.createAt*60000);
            o.createAt=date2str(dt);
            o.status=sta2icon(o.status);
            orders.push(o);
        }
        this.orders=orders;
        this.page.order=Math.ceil(resp.data.total/pgSize);
    });
},
query_contacts(pg) {
    var pgSize=this.service.N_SMPG;
    var offset=(parseInt(pg)-1)*pgSize;
    var url="/api/contact/list?customer="+this.id+"&offset="+offset+"&num="+pgSize;
    request({method:"GET",url:url}, this.service.name).then(resp=>{
        if(resp.code!=0||resp.data.total==0) {
            return;
        }
        var contacts=[];
        var dt=new Date();
        for(var c of resp.data.contacts) {
            dt.setTime(c.createAt*60000);
            contacts.push({id:c.id,name:c.name,post:c.post,
            createAt:date2str(dt),creator:c.creator});
        }
        this.contacts=contacts;
        this.page.contact=Math.ceil(resp.data.total/pgSize);
    });
},
query_touchlogs(pg) {
    var pgSize=this.service.N_SMPG;
    var offset=(parseInt(pg)-1)*pgSize;
    var url="/api/touchlog/custTouchlogs?customer="+this.id+"&offset="+offset+"&num="+pgSize;
    request({method:"GET",url:url}, this.service.name).then(resp=>{
        if(resp.code!=RetCode.OK||resp.data.total==0) {
            this.touchlogs=[];
            this.page.touchlog=0;
            return;
        }
        var logs=[];
        var dt=new Date();
        for(var l of resp.data.touchlogs) {
            dt.setTime(l.createAt*60000);
            logs.push({name:l.name,comment:l.comment,createAt:dt.toLocaleString(),
            t:l.createAt/*用于删除修改*/,cid:l.contact,creator:l.creator});
        }
        this.touchlogs=logs;
        this.page.touchlog=Math.ceil(resp.data.total/pgSize);
    });
},
query_shares() {
    var url="/api/customer/shareList?id="+this.id;
    request({method:"GET",url:url}, this.service.name).then(resp=>{
        if(resp.code!=0) {
            this.shares=[];
            return;
        }
        var shares=[];
        var dt=new Date();
        var year=dt.getFullYear();
        var t1,t2;
        resp.data.list.forEach(function(s) { //account,update_time,endT
            dt.setTime(s.endT*60000);
            t1=dt.getFullYear()-year>100?this.tags.forever:date2str(dt);
            dt.setTime(s.update_time);
            t2=date2str(dt);
            shares.push({account:s.account,endT:t1,createAt:t2,power:this.tags.share[s.power]});
        }.bind(this));
        this.shares=shares;
    });
},
create_order() {
    var dta=copyObj(this.newOrder,['price','nextSigners',"skus"]);
    if(dta.skus.length==0) {
        this.$refs.errMsg.showErr(5114, "no sku list");
        return;
    }
    dta.customer=this.id;
    dta.pid=this.prjInput.id;
    dta.prjName=this.prjInput.name;
    dta.comment=encodeExt(this.newOrder.ext);
    var url="/api/order/create";
    request({method:"POST",url:url,data:dta}, this.service.name).then(resp=>{
        if(resp.code != 0) {
            this.$refs.errMsg.showErr(resp.code, resp.info);
            return;
        }
        this.visible.newOrd=false;
        this.newOrder={pid:'',price:0,nextSigners:[],ext:{}};
        this.query_orders(1);
    })
},
create_contact() {
    var dta=copyObj(this.newContact,['name','address','phone','sex','level','post']);
    dta['customer']=this.id;
    dta['comment']=encodeExt(this.newContact.ext);
    dta['birthday']=Math.ceil(new Date(this.newContact.birthday).getTime()/86400000); //转为天数
    var opts={method:"POST",url:"/api/contact/add",data:dta};
    request(opts, this.service.name).then(resp=>{
        if(resp.code != 0) {
            this.$refs.errMsg.showErr(resp.code, resp.info);
        } else {
            this.visible.newContact=false;
            this.newContact={name:'',sex:0,level:0,phone:'',address:'',post:'',
                birthday:date2str(new Date()),ext:{}};
            this.query_contacts(1);
        }
    })
},
opr_touchlog(opr){
    var opts;
    if(opr=='add') { //增加
        var dta={contact:this.newTl.cid,comment:this.newTl.cmt};
        opts={method:"POST",url:"/api/touchlog/add",data:dta};
    } else if(opr=='update'){ //修改
        var dta={contact:this.newTl.cid,createAt:this.newTl.t,comment:this.newTl.cmt};
        opts={method:"PUT",url:"/api/touchlog/modify",data:dta}
    } else { //删除
        opts={method:"DELETE",url:"/api/touchlog/remove?contact="+this.newTl.cid+"&createAt="+this.newTl.t};
    }

    request(opts, this.service.name).then(resp=>{
        if(resp.code != RetCode.OK) {
            this.$refs.errMsg.showErr(resp.code, resp.info);
        } else {
            this.visible.newTl=false;
            this.newTl={t:0,act:'',cid:0,cmt:''};
            this.query_touchlogs(1);
        }
    })
},
customer_flow(){
    var url='/workflow?flow='+this.dtl.flowid
    +"&did="+this.id+"&flName=customer"
    +"&dtlApi="+encodeURIComponent("/customer/detail");
    this.$router.push(url);
},
save_base() {
    var cmt=encodeExt(this.ext);
    var url="/api/customer/setInfo";
    var req={id:this.id, name:this.dtl.name, comment:cmt,
     address:this.dtl.address, business:this.dtl.business};
    request({method:"POST",url:url,data:req}, this.service.name).then(resp=>{
        if(resp.code != 0) {
            this.$refs.errMsg.showErr(resp.code, resp.info);
            return;
        }
        this.visible.editBase=false;
    })
},
open_create_order() {
    var defaultVal={cmt:{n:this.tags.cmt,t:'s'}};
    var url="/api/proxy/gettemplate?name=order";
    this.ibf.template('order', url, defaultVal).then(tmpl=> {
        this.newOrder.price='';
        this.newOrder.ext=decodeExt("{}", tmpl);
        this.skuInput={sku:{},num:'',price:this.tags.order.skuPrice,suppliers:[]}
        this.visible.newOrd=true;
    });
},
open_new_contact() {
    var defaultVal={cmt:{n:this.tags.cmt,t:'s'}};
    var url="/api/proxy/gettemplate?name=contact";
    this.ibf.template('contact', url, defaultVal).then(tmpl=> {
        this.newContact.ext=decodeExt("{}", tmpl)
        this.visible.newContact=true;
    });
},
open_touchlog(i) {
    if(typeof i === 'number' && !isNaN(i)) {
        var t=this.touchlogs[i];
        this.newTl={n:t.name,t:t.t, cmt:t.comment, act:'update',cid:t.cid};
    } else {
        this.newTl={n:i.name,t:0,cid:i.id, act:'add'};
    }
    this.visible.newTl=true;
},
more_contacts() {
    this.visible.contact=!this.visible.contact;
    if(this.visible.contact && this.contacts.length==0) {
        this.query_contacts(1);
    }
},
more_orders() {
    this.visible.order=!this.visible.order;
    if(this.visible.order && this.orders.length==0) {
        this.query_orders(1);
    }
},
more_touchlogs() {
    this.visible.touchlog=!this.visible.touchlog;
    if(this.visible.touchlog && this.touchlogs.length==0) {
        this.query_touchlogs(1);
    }
},
more_shares() {
    this.visible.share=!this.visible.share;
    if(this.visible.share && this.shares.length==0) {
        this.query_shares();
    }
},
share_create(){
    if(this.newShare.to.length<=0){return;}
    var t=new Date(this.newShare.endT).getTime()/60000;
    var opts={method:"POST",url:"/api/customer/share",data:{id:this.id, endT:t,
     to:this.newShare.to, power:this.newShare.power}};
    request(opts, this.service.name).then(resp=>{
        if(resp.code != 0) {
            this.$refs.errMsg.showErr(resp.code, resp.info);
            return;
        }
        this.visible.newShare=false;
        this.query_shares();
    })
},
share_remove(acc){
    var opts={method:"POST",url:"/api/customer/unshare",data:{id:this.id,to:acc}};
    request(opts, this.service.name).then(resp=>{
        if(resp.code != 0) {
            this.$refs.errMsg.showErr(resp.code, resp.info);
        }
        this.query_shares();
    })
},
customer_deliver(){
    if(this.newShare.to.length<=0){return;}
    var opts={method:"POST",url:"/api/customer/deliver",data:{id:this.id, to:this.newShare.to[0]}};
    request(opts, this.service.name).then(resp=>{
        if(resp.code != 0) {
            this.$refs.errMsg.showErr(resp.code, resp.info);
            return;
        }
        this.service.back();
    })
},
menu_remove(){
    var msg=this.tags.cfmToDel+this.tags.customer.title+' "'+this.dtl.name+'"';
    this.$refs.confirmDlg.show(msg, ()=>{
        var opts={method:"DELETE",url:"/api/customer/remove?id="+this.id};
        request(opts, this.service.name).then(resp=>{
            if(resp.code != 0) {
                this.$refs.errMsg.showErr(resp.code, resp.info);
            }else{
                this.service.back();
            }
        })
    });
},
show_relations(){
    this.visible.relation=!this.visible.relation;
    if(!this.visible.relation) {
        return;
    }
    if(!this.relationChart) {
        this.relationChart=Vue.markRaw(echarts.init(document.getElementById('relationChart')));
    }
    var url="/api/relation/custRelations?customer="+this.id;
    request({method:"GET",url:url}, this.service.name).then(resp=>{
        if(resp.code != 0) {
            this.$refs.errMsg.showErr(resp.code, resp.info);
            return;
        }
        var categories=this.tags.levels.map(function(l){
            return {name:l};
        })
        var nodes=resp.data.nodes.map(function(n){
            return {id:''+n.id,name:n.name,category:n.level,symbolSize:(1+n.level)*5,label:{show:true}};
        })
        var labelCfg={show:true,formatter:function(p){return p.data.comment}}
        var links=resp.data.links.map(function(l){
            return {source:''+l.source,target:''+l.target,comment:l.comment,label:labelCfg};
        })
        this.relationChart.setOption({
            title: {show:false},
            tooltip: {},
            legend: [{data: this.tags.levels}],
            series: [{
                type: 'graph',
                layout: 'circular',
                //circular: {rotateLabel: true},
                data: nodes,
                links: links,
                categories: categories,
                roam: true,
                label: {position:'right',formatter:'{b}'},
                lineStyle: {color:'source',curveness: 0.3}
           }]
        })
    })
},
rmv_order_sku(i){
    var sku=this.newOrder.skus[i];
    var price=this.newOrder.price;
    price-=sku.price*sku.num;
    this.newOrder.price=price.toFixed(2);
    this.newOrder.skus.splice(i,1);
},
add_order_sku(){
    var sku = this.skuInput;
    this.newOrder.skus.push({sku:sku.sku.id, skuName:sku.sku.name,
        num:sku.num, price:sku.price, cmt:sku.cmt});
    var total=0;
    for(var s of this.newOrder.skus) {
        total+=s.price*s.num;
    }
    this.newOrder.price=total.toFixed(2);
},
get_suppliers() {
    if(!this.skuInput.sku.id) {
        this.skuInput.suppliers=[];
        return;
    }
    var opts={method:"GET", url:"/sku/listSupplier?id="+this.skuInput.sku.id};
    request(opts, this.ibf.SERVICE_RES).then(resp => {
        if(resp.code != RetCode.OK) {
            this.skuInput.suppliers=[];
            this.$refs.alertDlg.showErr(resp.code, resp.info);
            return;
        }
        this.skuInput.suppliers=resp.data.list;
    }); 
}
},
template:`
<q-layout view="hHh lpr fFf">
  <q-header>
    <q-toolbar>
      <q-btn flat round icon="arrow_back" dense @click="service.back"></q-btn>
      <q-toolbar-title>{{dtl.name}}</q-toolbar-title>
      <q-btn flat round dense icon="menu" v-if="dtl.power=='O'">
       <q-menu>
       <q-list style="min-width: 100px">
        <q-item clickable v-close-popup @click="visible.deliver=true">
          <q-item-section avatar><q-icon name="screen_share"></q-icon></q-item-section>
          <q-item-section>{{tags.menu.deliver}}</q-item-section>
        </q-item>
        <q-item clickable v-close-popup @click="menu_remove">
          <q-item-section avatar><q-icon name="delete"></q-icon></q-item-section>
          <q-item-section>{{tags.menu.remove}}</q-item-section>
        </q-item>
       </q-list>
      </q-menu>
     </q-btn>
    </q-toolbar>
  </q-header>

  <q-page-container>
    <q-page class="q-px-none q-pb-lg">
<q-banner dense inline-actions class="q-mb-md text-dark bg-blue-grey-1" dense>
{{tags.baseInfo}}
  <template v-slot:action>
   <q-icon name="edit" color="primary" @click.stop="visible.editBase=true" v-if="dtl.power=='O'"></q-icon>
  </template>
</q-banner>
<q-list dense>
  <q-item v-for="i in visSegs">
    <q-item-section>{{tags.customer[i]}}</q-item-section>
    <q-item-section>{{dtl[i]}}</q-item-section>
  </q-item>
  <q-item v-if="dtl.power=='O'||dtl.power=='W'" clickable @click.stop="customer_flow">
    <q-item-section>{{tags.customer.status}}</q-item-section>
    <q-item-section><q-icon :name="dtl.icon" color="blue"></q-icon></q-item-section>
  </q-item>
  <q-item v-if="dtl.power=='O'" clickable @click.stop="show_relations">
    <q-item-section>{{tags.contactRelations}}</q-item-section>
    <q-item-section><q-icon name="people" color="primary"></q-icon></q-item-section>
  </q-item>
  <q-item v-for="e in ext">
    <q-item-section>{{e.n}}</q-item-section>
    <q-item-section>{{e.v}}</q-item-section>
  </q-item>
</q-list>

<!-- 联系人列表 -->
<q-banner dense inline-actions class="q-mb-sm text-dark bg-blue-grey-1" @click="more_contacts" dense>
{{tags.contact.title}}
  <template v-slot:action>
    <q-icon name="add_circle" color="primary" @click.stop="open_new_contact"></q-icon>
  </template>
</q-banner>
<div v-show="visible.contact">
<q-list separator>
  <q-item v-for="c in contacts" dense clickable @click="service.goto('/contact?id='+c.id)">
    <q-item-section>{{c.name}}</q-item-section>
    <q-item-section>{{c.post}}</q-item-section>
    <q-item-section>{{c.creator}}</q-item-section>
    <q-item-section>{{c.createAt}}</q-item-section>
    <q-item-section avatar>
     <q-icon :name="tags.icons['touchlog']" @click.stop="open_touchlog(c)" color="primary"></q-icon>
    </q-item-section>
  </q-item>
</q-list>
<div class="q-pa-sm flex flex-center" v-if="page.contact>1">
 <q-pagination color="primary" :max="page.contact" max-pages="10" v-model="page.curContact"
  dense boundary-numbers="false" @update:model-value="query_contacts"></q-pagination>
</div>
</div>

<!-- 联系记录列表 -->
<q-banner dense inline-actions class="q-mb-sm text-dark bg-blue-grey-1" @click="more_touchlogs" dense>
{{tags.touchlog}}
</q-banner>
<div v-show="visible.touchlog">
<q-list separator>
 <q-item v-for="(t,i) in touchlogs" dense clickable @click="open_touchlog(i)">
  <q-item-section avatar>{{t.name}}</q-item-section>
  <q-item-section>{{t.comment}}</q-item-section>
  <q-item-section>{{t.creator}}</q-item-section>
  <q-item-section side>{{t.createAt}}</q-item-section>
 </q-item>
</q-list>
<div class="q-pa-sm flex flex-center" v-if="page.touchlog>1">
 <q-pagination color="primary" :max="page.touchlog" max-pages="10" v-model="page.curTl"
 dense boundary-numbers="false" @update:model-value="query_touchlogs"></q-pagination>
</div>
</div>

<!-- 订单列表 -->
<q-banner dense inline-actions class="q-mb-sm text-dark bg-blue-grey-1" @click="more_orders" dense>
{{tags.order.title}}
  <template v-slot:action>
    <q-icon name="add_circle" color="primary" @click.stop="open_create_order"></q-icon>
  </template>
</q-banner>
<q-list separator v-show="visible.order">
 <q-item v-for="o in orders" dense clickable @click="service.goto('/order?id='+o.id)">
  <q-item-section>{{o.creator}}</q-item-section>
  <q-item-section>{{o.price}}/{{o.payment}}</q-item-section>
  <q-item-section>{{o.createAt}}</q-item-section>
  <q-item-section avatar>
   <q-icon :name="o.status" color="primary"></q-icon>
  </q-item-section>
 </q-item>
</q-list>
<div class="q-pa-sm flex flex-center" v-if="page.order>1">
 <q-pagination color="primary" :max="page.order" max-pages="10" v-model="page.curOrder"
  dense boundary-numbers="false" @update:model-value="query_orders"></q-pagination>
</div>

<div v-if="dtl.power=='O'">
<!-- 分享列表 -->
<q-banner dense inline-actions class="q-mb-sm text-dark bg-blue-grey-1" @click="more_shares" dense>
{{tags.share.title}}
<template v-slot:action>
   <q-icon name="add_circle" color="primary" @click.stop="visible.newShare=true"></q-icon>
</template>
</q-banner>
<q-list separator dense v-show="visible.share">
 <q-item clickable v-for="s in shares" dense>
  <q-item-section>{{s.account}}</q-item-section>
  <q-item-section>{{s.endT}}</q-item-section>
  <q-item-section>{{s.power}}</q-item-section>
  <q-item-section>{{s.createAt}}</q-item-section>
  <q-item-section thumbnail>
   <q-icon name="delete" color="red" @click="share_remove(s.account)"></q-icon>
  </q-item-section>
 </q-item>
</q-list>
</div>
<div id="relationChart" :style="{width:'90vw',height:'90vw'}" v-show="visible.relation"></div>
    </q-page>
  </q-page-container>
</q-layout>

<component-alert-dialog :title="tags.failToCall" :errMsgs="tags.errMsgs" ref="errMsg"></component-alert-dialog>
<component-confirm-dialog :title="tags.alert" :close="tags.cancel" :ok="tags.ok" ref="confirmDlg"></component-confirm-dialog>

<!-- 新建联系人弹窗 -->
<q-dialog v-model="visible.newContact" no-backdrop-dismiss>
  <q-card style="min-width:70vw">
    <q-card-section>
      <div class="text-h6">{{tags.addContact}}</div>
    </q-card-section>
    <q-card-section class="q-pt-none">
    <q-list>
      <q-item><q-item-section>
        <q-input :label="tags.contact.name" v-model="newContact.name" dense></q-input>
      </q-item-section></q-item>
      <q-item><q-item-section>
       <div class="row">
         <div class="col">{{tags.sex}}</div>
         <div class="col">
          <q-radio dense v-model="newContact.sex" val="M" :label="tags.sexName.M" color="indigo" keep-color></q-radio>
          <q-radio dense v-model="newContact.sex" val="F" :label="tags.sexName.F" color="pink" keep-color></q-radio>
         </div>
       </div>
      </q-item-section></q-item>
      <q-item><q-item-section><div class="row">
          <div class="col">{{tags.contactLevel}}</div>
          <div class="col">
            <q-rating v-model="newContact.level" max="5" size="1em"
             color="yellow" color-selected="orange"></q-rating>
          </div>
      </div></q-item-section></q-item>
      <q-item><q-item-section>
        <q-input :label="tags.contact.post" v-model="newContact.post" dense></q-input>
      </q-item-section></q-item>
      <q-item><q-item-section>
        <q-input :label="tags.contact.address" v-model="newContact.address" dense></q-input>
      </q-item-section></q-item>
      <q-item><q-item-section>
        <q-input :label="tags.contact.phone" v-model="newContact.phone" dense
        :rules="[v=>/^1[0-9]{10}$/.test(v)||tags.mobilePls]" maxlength=11></q-input>
      </q-item-section></q-item>
      <q-item><q-item-section>
       <component-date-input :label="tags.contact.birthday" v-model="newContact.birthday" max="today"></component-date-input>
      </q-item-section></q-item>
      <!-- ext/comment -->
      <q-item v-for="e in newContact.ext"><q-item-section>
        <div v-if="e.t=='d'">
          <component-date-input :close="tags.ok" :label="e.n" v-model="e.v"></component-date-input>
        </div>
        <div v-else-if="e.t=='b'">
          <q-checkbox v-model="e.v" :label="e.n" left-label></q-checkbox>
        </div>
        <div v-else>
         <q-input :label="e.n" v-model="e.v" dense :autogrow="e.t!='n'"
          :type="e.t=='n'?'number':'textarea'"></q-input>
        </div>
      </q-item-section></q-item>
    </q-list>
    </q-card-section>
    <q-card-actions align="right">
      <q-btn :label="tags.ok" color="primary" @click="create_contact"></q-btn>
      <q-btn flat :label="tags.close" color="primary" v-close-popup></q-btn>
    </q-card-actions>
  </q-card>
</q-dialog>

<!-- 新建订单弹窗 -->
<q-dialog v-model="visible.newOrd" no-backdrop-dismiss>
  <q-card style="min-width:70vw">
    <q-card-section>
      <div class="text-h6">{{tags.modify}}</div>
    </q-card-section>
    <q-card-section class="q-pt-none">
    <q-list>
     <q-item><q-item-section>
      <component-prj-selector v-model="prjInput" :label="tags.order.prj"></component-prj-selector>
     </q-item-section></q-item>
     <!-- ext/comment -->
     <q-item v-for="e in dtl.ext"><q-item-section>
        <div v-if="e.t=='d'">
          <component-date-input :close="tags.ok" :label="e.n" v-model="e.v"></component-date-input>
        </div>
        <div v-else-if="e.t=='b'">
          <q-checkbox v-model="e.v" :label="e.n" left-label></q-checkbox>
        </div>
        <div v-else>
         <q-input :label="e.n" v-model="e.v" dense :autogrow="e.t!='n'"
          :type="e.t=='n'?'number':'textarea'"></q-input>
        </div>
     </q-item-section></q-item>
     <q-item><q-item-section>
        <component-user-selector :label="tags.signers" :accounts="newOrder.nextSigners"></component-user-selector>
     </q-item-section></q-item>
     <q-item><q-item-section>
      <q-banner inline-actions class="bg-indigo-1 q-mt-sm" dense>
       {{tags.order.skuList}}
      </q-banner>
      <q-list dense separator>
      <q-item clickable v-for="(s,i) in newOrder.skus">
       <q-item-section>{{s.skuName}}</q-item-section>
       <q-item-section>{{s.num}}</q-item-section>
       <q-item-section side>{{s.price}}</q-item-section>
       <q-item-section side>
        <q-icon color="red" name="clear" @click="rmv_order_sku(i)"></q-icon>
       <q-item-section>
      </q-item>
      </q-list>
      <q-list dense>
       <q-item>
       <q-item-section>
        <component-sku-selector v-model="skuInput.sku" :label="tags.order.skuName" dense></component-sku-selector>
       </q-item-section>
       <q-item-section side>{{skuInput.price}}
        <q-popup-edit v-model="skuInput.price" v-slot="scope" @before-show="get_suppliers()">
         <q-input v-model.number="scope.value" dense autofocus @keyup.enter="scope.set" type="number">
           <template v-slot:append>
            <q-icon name="save" color="primary" @click="scope.set"></q-icon>
           </template>
         </q-input>
         <q-list dense>
           <q-item v-for="s in skuInput.suppliers" clickable @click="scope.value=s.price;scope.set()">
            <q-item-section>{{s.name}}</q-item-section>
            <q-item-section side>{{s.price}}</q-item-section>
           </q-item>
         </q-list>
        </q-popup-edit>
       </q-item-section>
       </q-item>
       <q-item>
       <q-item-section>
        <q-input v-model.number="skuInput.num" :label="tags.order.skuNum" dense type="number"></q-input>
       </q-item-section>
       <q-item-section side>
        <q-icon name="add_circle" @click="add_order_sku" color="primary"></q-icon>
       </q-item-section>
      </q-item>
      </q-list>
     
     </q-item-section></q-item>
     <q-item><q-item-section>
       <q-input :label="tags.order.price" v-model="newOrder.price" dense></q-input>
     </q-item-section></q-item>
    </q-list>
    </q-card-section>
    <q-card-actions align="right">
      <q-btn :label="tags.ok" color="primary" @click="create_order"></q-btn>
      <q-btn flat :label="tags.close" color="primary" v-close-popup></q-btn>
    </q-card-actions>
  </q-card>
</q-dialog>

<!-- 新建/修改/删除联系记录弹窗 -->
<q-dialog v-model="visible.newTl" no-backdrop-dismiss>
  <q-card style="min-width:70vw">
    <q-card-section>
      <div class="text-h6">{{newTl.n}}-{{tags.touchlog}}</div>
    </q-card-section>
    <q-card-section class="q-pt-none">
    <q-list>
     <q-item><q-item-section>
      <q-input :label="tags.touchCtnt" v-model="newTl.cmt" type="textarea" dense autogrow></q-input>
     </q-item-section></q-item>
    </q-list>
    </q-card-section>
    <q-card-actions class="row">
     <div class="col">
      <q-btn :label="tags.remove" flat color="red" @click="opr_touchlog('rmv')" v-show="newTl.tp==2"></q-btn>
     </div>
     <div class="col text-right">
      <q-btn :label="tags.ok" color="primary" @click="opr_touchlog(newTl.act)"></q-btn>
      <q-btn flat :label="tags.close" color="primary" v-close-popup></q-btn>
     </div>
    </q-card-actions>
  </q-card>
</q-dialog>

<!-- 修改客户基本信息弹窗 -->
<q-dialog v-model="visible.editBase" no-backdrop-dismiss>
  <q-card style="min-width:70vw">
    <q-card-section>
      <div class="text-h6">{{tags.baseInfo}}</div>
    </q-card-section>
    <q-card-section class="q-pt-none">
    <q-list>
      <q-item><q-item-section>
        <q-input :label="tags.customer.name" v-model="dtl.name" dense></q-input>
      </q-item-section></q-item>
      <q-item><q-item-section>
        <q-input :label="tags.customer.address" v-model="dtl.address" dense autogrow></q-input>
      </q-item-section></q-item>
      <q-item><q-item-section>
        <q-input :label="tags.customer.business" v-model="dtl.business" dense autogrow></q-input>
      </q-item-section></q-item>
      <!-- ext/comment -->
      <q-item v-for="e in dtl.ext"><q-item-section>
        <div v-if="e.t=='d'">
          <component-date-input :close="tags.ok" :label="e.n" v-model="e.v"></component-date-input>
        </div>
        <div v-else-if="tpl.t=='b'">
          <q-checkbox v-model="e.v" :label="e.n" left-label></q-checkbox>
        </div>
        <div v-else>
         <q-input borderless :label="e.n" v-model="e.v" dense :autogrow="e.t!='n'"
          :type="e.t=='n'?'number':'textarea'"></q-input>
        </div>
      </q-item-section></q-item>
    </q-list>
    </q-card-section>
    <q-card-actions align="right">
      <q-btn :label="tags.ok" color="primary" @click="save_base"></q-btn>
      <q-btn flat :label="tags.close" color="primary" v-close-popup></q-btn>
    </q-card-actions>
  </q-card>
</q-dialog>

<!-- 分享客户弹窗 -->
<q-dialog v-model="visible.newShare" no-backdrop-dismiss>
  <q-card style="min-width:70vw">
    <q-card-section>
      <div class="text-h6">{{dtl.name}}</div>
    </q-card-section>
    <q-card-section class="q-pt-none">
    <q-list>
      <q-item><q-item-section>
          <div class="q-gutter-sm">
         <q-radio dense v-model="newShare.power" val="S" :label="tags.share.S"></q-radio>
         <q-radio dense v-model="newShare.power" val="O" :label="tags.share.O" color="red" keep-color></q-radio>
        </div>
      </q-item-section></q-item>
      <q-item><q-item-section>
       <component-date-input :label="tags.share.endT" v-model="newShare.endT" :min="curDate"></component-date-input>
      </q-item-section></q-item>
      <q-item><q-item-section>
        <component-user-selector :label="tags.share.to" :accounts="newShare.to"></component-user-selector>
      </q-item-section></q-item>
    </q-list>
    </q-card-section>
    <q-card-actions align="right">
      <q-btn :label="tags.ok" color="primary" @click="share_create"></q-btn>
      <q-btn flat :label="tags.close" color="primary" v-close-popup></q-btn>
    </q-card-actions>
  </q-card>
</q-dialog>

<!-- 将客户转交给其他用户的弹窗 -->
<q-dialog v-model="visible.deliver" no-backdrop-dismiss>
  <q-card style="min-width:70vw">
    <q-card-section>
      <div class="text-h6">{{dtl.name}}</div>
    </q-card-section>
    <q-card-section class="q-pt-none">
    <q-list>
      <q-item><q-item-section>
        <component-user-selector :label="tags.share.to" :accounts="newShare.to"></component-user-selector>
      </q-item-section></q-item>
    </q-list>
    </q-card-section>
    <q-card-actions align="right">
      <q-btn :label="tags.ok" color="primary" @click="customer_deliver"></q-btn>
      <q-btn flat :label="tags.close" color="primary" v-close-popup></q-btn>
    </q-card-actions>
  </q-card>
</q-dialog>
`
}
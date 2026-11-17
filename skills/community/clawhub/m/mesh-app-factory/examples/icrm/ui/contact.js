import {encodeExt,decodeExt} from '/assets/v3/settings/config.js';

export default {
inject:['service', 'tags', 'ibf'],
data() {return {
    id:this.$route.query.id,
    dtl:{},//详情:id,name,cname,address,creator,createAt,birthday,sex,level,post,phone,comment
    ext:{}, //从联系人的comment转化而来
    dispSegs:["post","phone","cname","address","creator","createAt"],
    touchlogs:[], //comment,createAt,creator
    relations:[], //target,name,comment,createAt
    shares:[],
    contacts:[],//创建关系供选择的列表,id,name
    contactOpts:[],//创建关系供选择的列表,id,name
    curDate:'',//当前时间，用在分享界面
    
    newTlDta:{t:0,comment:'',tp:0},
    newRlDta:{comment:'',target:{}},
    newShare:{endT:'',to:[],power:"S"},
    
    page:{touchlog:0,curTl:1,relation:0,curRl:1},
    visible:{touchlog:false, touchlogDlg:false, relation:false, editBase:false,
         newRelation:false, share:false, newShare:false, remove:false}
}},
created(){
    this.curDate=date2str(new Date());
    var defaultVal={cmt:{n:this.tags.cmt,t:'s'}};
    var url="/api/proxy/gettemplate?name=contact";
    this.ibf.template('contact', url, defaultVal).then(tmpl=> {
        this.detail(tmpl);
    });
},
methods:{
detail(tmpl) {
    var reqUrl="/api/contact/detail?id="+this.id;
    request({method:"GET", url:reqUrl}, this.service.name).then(resp=>{
        if(!resp || resp.code != 0) {
            this.$refs.errMsg.showErr(resp.code, resp.info);
            return;
        }
        var dtl=resp.data;

        var dt=new Date();
        var year=dt.getFullYear();
        dt.setTime(dtl.createAt*60000);
        dtl.createAt=date2str(dt);

        if(dtl.power!='O') {//不是联系人的所有人，是客户的所有人也可以修改、删除
            dtl.power=dtl.custPower;
        }
        
        dt.setTime(dtl.birthday*86400000);
        dtl.birthday=date2str(dt);
        dtl.age=year-dt.getFullYear();
        
        dtl.sex=dtl.sex;
        dtl.sex_s=this.tags.sexName[dtl.sex];
        this.ext=decodeExt(dtl.comment, tmpl);
        this.dtl = dtl;
    });
},
query_touchlogs(pg) {
    var offset=(parseInt(pg)-1)*this.service.N_PAGE;
    var url="/api/touchlog/list?contact="+this.id+"&offset="+offset+"&num="+this.service.N_PAGE;
    request({method:"GET",url:url}, this.service.name).then(resp=>{
        if(resp.code!=0||resp.data.total==0) {
            return;
        }
        var logs=[];
        var dt=new Date();
        for(var i in resp.data.touchlogs) { //createAt,creator,comment
            var l=resp.data.touchlogs[i];
            dt.setTime(l.createAt*60000);
            logs.push({creator:l.creator,comment:l.comment,createAt:datetime2str(dt),
             t:l.createAt/*用于修改删除*/});
        }
        this.touchlogs=logs;
        this.page.touchlog=Math.ceil(resp.data.total/this.service.N_PAGE);
    });
},
query_relations() {
    var url="/api/relation/list?customer="+this.dtl.customer+"&contact="+this.id;
    request({method:"GET",url:url}, this.service.name).then(resp=>{
        if(resp.code!=0) {
            this.relations=[];
            return;
        }
        var dt=new Date();
        var relations=resp.data.relations.map(function(r) { //target,name,comment,update_time
            dt.setTime(r.update_time);
            return {createAt:datetime2str(dt),comment:r.comment,name:r.name,target:r.target};
        });
        this.relations=relations;
    });
},
query_shares() {
    var url="/api/contact/shareList?id="+this.id;
    request({method:"GET",url:url}, this.service.name).then(resp=>{
        if(resp.code!=0) {
            this.shares=[];
            return;
        }
        var dt=new Date();
        var year=dt.getFullYear();
        var t1,t2;
        var shares=resp.data.list.map((s)=> { //account,update_time,endT
            dt.setTime(s.endT*60000);
            t1=dt.getFullYear()-year>100?this.tags.forever:datetime2str(dt);
            dt.setTime(s.update_time);
            t2=datetime2str(dt);
            return {account:s.account,endT:t1,createAt:t2,power:this.tags.share[s.power]};
        });
        this.shares=shares;
    });
},
opr_touchlog(opr){
    var opts;
    if(opr==1){
        var dta={contact:this.id,comment:this.newTlDta.comment};
        opts={method:"POST",url:"/api/touchlog/add",data:dta}
    } else if(opr==2){
        var dta={contact:this.id,createAt:this.newTlDta.t,comment:this.newTlDta.comment};
        opts={method:"PUT",url:"/api/touchlog/modify",data:dta}
    } else {
        opts={method:"DELETE",url:"/api/touchlog/remove?contact="+this.id+"&createAt="+this.newTlDta.t}
    }
    request(opts, this.service.name).then(resp=>{
        if(resp.code != 0) {
            this.$refs.errMsg.showErr(resp.code, resp.info);
        } else {
            this.visible.touchlogDlg=false;
            this.newTlDta={t:0,tp:0,comment:''};
            this.query_touchlogs(1);
        }
    })
},
open_relation_dlg() {
    this.newRlDta={comment:'',target:null};
    if(this.contacts.length>0) {
        this.visible.newRelation=true;
        return;
    }
    var url="/api/contact/custList?customer="+this.dtl.customer;
    request({method:"GET",url:url}, this.service.name).then(resp=>{
        if(resp.code != 0) {
            return;
        }
        this.contacts=resp.data.contacts;
        this.visible.newRelation=true;
    })
},
filterContacts(val, update, abort) {//用于建立关系时，过滤联系人选项
    update(()=>{
      if(val.length<1) {
          abort()
          return
      }
      var s = val.toLowerCase()
      var opts=[];
      var curC=this.id;
      this.contacts.forEach(c=>{
        if(c.id!=curC&&c.name.toLowerCase().indexOf(s) >= 0){
          opts.push({label:c.name,value:c.id});
        }
      });
      this.contactOpts = opts;
    });
},
add_relation(){
    var dta={customer:this.dtl.customer,contact:this.id,target:this.newRlDta.target.value,comment:this.newRlDta.comment};
    var opts={method:"POST",url:"/api/relation/add",data:dta};
    request(opts, this.service.name).then(resp=>{
        if(resp.code != 0) {
            this.$refs.errMsg.showErr(resp.code, resp.info);
            return;
        }
        this.visible.newRelation=false;
        this.query_relations();
    })
},
remove_relation(target){
    var opts={method:"DELETE",url:"/api/relation/remove?contact="+this.id+"&customer="+this.dtl.customer+"&target="+target};
    request(opts, this.service.name).then(resp=>{
        if(resp.code != 0) {
            this.$refs.errMsg.showErr(resp.code, resp.info);
            return;
        }
        this.visible.newRelation=false;
        this.query_relations();
    })
},
save_base() {
    var dta=copyObj(this.dtl,['name','address','phone','sex','level','post']);
    dta.comment=encodeExt(this.ext);
    dta.birthday=Math.ceil(new Date(this.dtl.birthday).getTime()/86400000); //转为天数
    dta.id=this.id;

    var url="/api/contact/modify";
    request({method:"POST",url:url,data:dta}, this.service.name).then(resp=>{
        if(resp.code != 0) {
            this.$refs.errMsg.showErr(resp.code, resp.info);
            return;
        }
        this.visible.editBase=false;
    })
},
more_touchlogs() {
    this.visible.touchlog=!this.visible.touchlog;
    if(this.visible.touchlog && this.touchlogs.length==0) {
        this.query_touchlogs(1);
    }
},
more_relations() {
    this.visible.relation=!this.visible.relation;
    if(this.visible.relation && this.relations.length==0) {
        this.query_relations();
    }
},
more_shares() {
    this.visible.share=!this.visible.share;
    if(this.visible.share && this.shares.length==0) {
        this.query_shares();
    }
},
share_create(){
    var t=parseInt(new Date(this.newShare.endT).getTime()/60000);
    var url="/api/contact/share";
    var req={id:this.id, endT:t, to:this.newShare.to, power:this.newShare.power};
    request({method:"POST",url:url,data:req}, this.service.name).then(resp=>{
        if(resp.code != 0) {
            this.$refs.errMsg.showErr(resp.code, resp.info);
            return;
        }
        this.visible.newShare=false;
        this.query_shares();
    })
},
share_remove(acc){
    var opts={method:"POST",url:"/api/contact/unshare",data:{id:this.id,to:acc}};
    request(opts, this.service.name).then(resp=>{
        if(resp.code != 0) {
            this.$refs.errMsg.showErr(resp.code, resp.info);
        }
        this.query_shares();
    })
},
menu_remove(){
    var msg=this.tags.cfmToDel+this.tags.contact.title+' "'+this.dtl.name+'"';
    this.$refs.confirmDlg.show(msg, ()=>{
        var opts={method:"DELETE",url:"/api/contact/remove?id="+this.id};
        request(opts, this.service.name).then((resp)=>{
            if(resp.code != 0) {
                this.$refs.errMsg.showErr(resp.code, resp.info);
            }else{
                this.service.back();
            }
        })
    })
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

<q-banner dense inline-actions class="q-mb-md text-dark bg-blue-grey-1">
{{tags.baseInfo}}
  <template v-slot:action>
    <q-icon name="edit" color="primary" @click.stop="visible.editBase=true" v-if="dtl.power=='O'"></q-icon>
  </template>
</q-banner>
<q-list dense>
  <q-item>
   <q-item-section>{{tags.contact.name}}</q-item-section>
   <q-item-section>{{dtl.name}}</q-item-section>
  </q-item>
  <q-item>
   <q-item-section>{{tags.contact.sex}}</q-item-section>
   <q-item-section>{{dtl.sex_s}}</q-item-section>
  </q-item>
  <q-item>
   <q-item-section>{{tags.contact.level}}</q-item-section>
   <q-item-section><q-rating v-model="dtl.level" disable max="5" size="sm" color="yellow" color-selected="orange"></q-rating></q-item-section>
  </q-item>
  <q-item>
   <q-item-section>{{tags.contact.birthday}}</q-item-section>
   <q-item-section>{{dtl.birthday}}({{dtl.age}}{{tags.yearsOld}})</q-item-section>
  </q-item>
  <q-item v-for="i in dispSegs">
    <q-item-section>{{tags.contact[i]}}</q-item-section>
    <q-item-section>{{dtl[i]}}</q-item-section>
  </q-item>
  <q-item v-for="e in ext">
    <q-item-section>{{e.n}}</q-item-section>
    <q-item-section>{{e.v}}</q-item-section>
  </q-item>
</q-list>

<!-- 联系记录列表 -->
<q-banner dense inline-actions class="q-mb-sm text-dark bg-blue-grey-1" @click="more_touchlogs">
{{tags.touchlog}}
  <template v-slot:action>
    <q-icon name="add_circle" color="primary" @click.stop="newTlDta={t:0,tp:1,comment:''};visible.touchlogDlg=true"></q-icon>
  </template>
</q-banner>
<div v-show="visible.touchlog">
<q-list separator dense v-show="visible.touchlog">
 <q-item clickable v-for="t in touchlogs" dense @click="newTlDta={t:t.t,tp:2,comment:t.comment};visible.touchlogDlg=true">
  <q-item-section avatar>{{t.creator}}</q-item-section>
  <q-item-section>{{t.comment}}</q-item-section>
  <q-item-section side>{{t.createAt}}</q-item-section>
 </q-item>
</q-list>
<div class="q-pa-sm flex flex-center" v-if="page.touchlog>1">
 <q-pagination color="primary" :max="page.touchlog" max-pages="10" v-model="page.curTl"
 dense boundary-numbers="false" @update:model-value="query_touchlogs"></q-pagination>
</div>
</div>

<!-- 关系列表 -->
<q-banner dense inline-actions class="q-mb-sm text-dark bg-blue-grey-1" @click="more_relations">
{{tags.relations}}
  <template v-slot:action>
    <q-icon name="add_circle" color="primary" @click.stop="open_relation_dlg"></q-icon>
  </template>
</q-banner>
<div v-show="visible.relation">
<q-list separator dense>
 <q-item clickable v-for="r in relations" dense>
  <q-item-section>{{r.name}}</q-item-section>
  <q-item-section>{{r.comment}}</q-item-section>
  <q-item-section>{{r.createAt}}</q-item-section>
  <q-item-section thumbnail>
   <q-icon name="delete" color="red" @click="remove_relation(r.target)"></q-icon>
  </q-item-section>
 </q-item>
</q-list>
</div>

<!-- 分享列表 -->
<div v-if="dtl.power=='O'">
<q-banner dense inline-actions class="q-mb-sm text-dark bg-blue-grey-1" @click="more_shares">
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
    </q-page>
  </q-page-container>
</q-layout>

<component-alert-dialog :title="tags.failToCall" :errMsgs="tags.errMsgs" ref="errMsg"></component-alert-dialog>
<component-confirm-dialog :title="tags.alert" :close="tags.cancel" :ok="tags.ok" ref="confirmDlg"></component-confirm-dialog>

<!-- 新建/修改/删除联系记录弹窗 -->
<q-dialog v-model="visible.touchlogDlg" no-backdrop-dismiss>
  <q-card style="min-width:70vw">
    <q-card-section>
      <div class="text-h6">{{tags.touchlog}}</div>
    </q-card-section>
    <q-card-section class="q-pt-none">
    <q-list>
      <q-item><q-item-section>
        <q-input :label="tags.touchCtnt" v-model="newTlDta.comment" type="textarea"
        dense autogrow></q-input>
      </q-item-section></q-item>
    </q-list>
    </q-card-section>
    <q-card-actions class="row">
      <div class="col">
       <q-btn :label="tags.remove" flat color="red" @click="opr_touchlog(3)" v-show="newTlDta.tp==2"></q-btn>
      </div>
      <div class="col text-right">
       <q-btn :label="tags.ok" color="primary" @click="opr_touchlog(newTlDta.tp)"></q-btn>
       <q-btn flat :label="tags.close" color="primary" v-close-popup></q-btn>
      </div>
    </q-card-actions>
  </q-card>
</q-dialog>

<!-- 新建关系记录弹窗 -->
<q-dialog v-model="visible.newRelation" no-backdrop-dismiss>
  <q-card style="min-width:70vw">
    <q-card-section>
      <div class="text-h6">{{tags.relations}}</div>
    </q-card-section>
    <q-card-section class="q-pt-none">
    <q-list>
      <q-item><q-item-section>
       <q-select v-model="newRlDta.target" use-input use-chips
        input-debounce=200 :options="contactOpts" @filter="filterContacts" dense></q-select>
      </q-item-section></q-item>
      <q-item><q-item-section>
        <q-input :label="tags.relationCmt" v-model="newRlDta.comment" dense></q-input>
      </q-item-section></q-item>
    </q-list>
    </q-card-section>
    <q-card-actions align="right">
      <q-btn :label="tags.ok" color="primary" @click="add_relation"></q-btn>
      <q-btn flat :label="tags.close" color="primary" v-close-popup></q-btn>
    </q-card-actions>
  </q-card>
</q-dialog>

<!-- 修改联系人基本信息弹窗 -->
<q-dialog v-model="visible.editBase" no-backdrop-dismiss>
  <q-card style="min-width:70vw">
    <q-card-section>
      <div class="text-h6">{{tags.baseInfo}}</div>
    </q-card-section>
    <q-card-section class="q-pt-none">
    <q-list dense>
      <q-item><q-item-section>
        <q-input :label="tags.contact.name" v-model="dtl.name" dense></q-input>
      </q-item-section></q-item>
      <q-item><q-item-section>
       <div class="row">
        <div class="col">{{tags.sex}}</div>
        <div class="col">
          <q-radio dense v-model="dtl.sex" val="M" :label="tags.sexName.M" color="indigo" keep-color></q-radio>
          <q-radio dense v-model="dtl.sex" val="F" :label="tags.sexName.F" color="pink" keep-color></q-radio>
        </div>
       </div>
      </q-item-section></q-item>
      <q-item><q-item-section>
       <div class="row">
        <div class="col">{{tags.contactLevel}}</div>
         <div class="col q-pa-xs">
          <q-rating v-model="dtl.level" max="5" size="1em"
           color="yellow" color-selected="orange"></q-rating>
        </div>
       </div>
      </q-item-section></q-item>
      <q-item><q-item-section>
        <q-input :label="tags.contact.post" v-model="dtl.post" dense></q-input>
      </q-item-section></q-item>   
      <q-item><q-item-section>
        <q-input :label="tags.contact.phone" v-model="dtl.phone" dense></q-input>
      </q-item-section></q-item>
      <q-item><q-item-section>
        <q-input :label="tags.contact.address" v-model="dtl.address" dense></q-input>
      </q-item-section></q-item>   
      <q-item><q-item-section>
       <component-date-input :close="tags.ok" :label="tags.contact.birthday" v-model="dtl.birthday" max="today"></component-date-input>
      </q-item-section></q-item>
      <q-item v-for="e in ext"><q-item-section>
        <div v-if="e.t=='d'">
         <component-date-input :close="tags.ok" :label="e.n" v-model="e.v"></component-date-input>
        </div>
        <div v-else-if="e.t=='b'">
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

<!-- 分享联系人弹窗 -->
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
`
}
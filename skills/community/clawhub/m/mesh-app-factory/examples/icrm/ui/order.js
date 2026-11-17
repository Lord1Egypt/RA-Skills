import BankSelector from "/ibfbase/components/bank_selector.js";
import UserInput from "/assets/v3/components/user_input.js";
import DatetimeInput from "/assets/v3/components/datetime_input.js";
import {sta2icon} from '/assets/v3/components/workflow.js';
import {_WF_} from "/assets/v3/components/workflow.js"
import {encodeExt,decodeExt} from '/assets/v3/settings/config.js';

const EMPTY_PUR={expDate:'',descr:'',type:'SELL',receiver:'',buyer:[]};
const EMPTY_BUSI={order:0,account:'',uid:0,cmt:'',reason:'',dest:'',start:'',end:''};

export default {
components:{
    "bank-select":BankSelector,
    "user-input":UserInput,
    "datetime-input":DatetimeInput
},
inject:['service', 'tags', 'ibf'],
data() {return {
    id:this.$route.query.id,
    //customer,cname,price,skuId,skuName,skuPrice,creator,createAt,
    //flowid,status,comment,fileNo,taxid,cost
    dtl:{},
    ext:[], //从订单的comment转化而来
    
    costs:[], //id,budget,createAt,creator
    payments:[], //id,amount,createAt,creator
    purList:[], //订单相关的采购
    busiList:[], //订单相关的差旅

    newCost:{cost:0,nextSigners:[],comment:'',ext:[]},
    newPayment:{amount:0,bank:'',comment:'',ext:[]},
    purchase:{visible:false,dlg:false,dta:{},skus:[],sku:{sku:{},num:''}},
    business:{visible:false,dlg:false,dta:{}},
    userInput:{uid:0,account:''},

    visSegs:["taxid","price","payment","creator","createAt"],
    editBase:false,
    payment:{visible:false,dlg:false,cur:1,max:0},
    cost:{tmpl:{},tpOpts:[],visible:false,dlg:false,max:0,cur:1}
}},
created(){
    var defaultVal={cmt:{n:this.tags.cmt,t:'s'}};
    var url="/api/proxy/gettemplate?name=order";
    this.ibf.template('order', url, defaultVal).then(tmpl=> {
        this.detail(tmpl);
    });
    var defaultVal={cmt:{n:this.tags.cmt,t:'s'}};
    var url="/api/proxy/gettemplate?name=cost";
    this.ibf.template('cost', url, defaultVal).then(tmpl=> {
        this.cost.tmpl=tmpl
    })
    var types=this.tags.cost.types;
    this.cost.tpOpts=[
        {label:types.GIFT,value:'GIFT'},
        {label:types.SERV,value:'SERV'},
        {label:types.OTH,value:'OTH'}
    ];
},
methods:{
detail(tmpl) {
    var reqUrl="/api/order/detail?id="+this.id;
    request({method:"GET", url:reqUrl},this.service.name).then(resp=>{
        if(!resp || resp.code != 0) {
            this.$refs.errMsg.showErr(resp.code, resp.info);
            return;
        }
        var dtl=resp.data;
        dtl.createAt=date2str(new Date(dtl.createAt*60000));
        dtl.icon=sta2icon(dtl.status);
        dtl.needPay=dtl.price-dtl.payment;
        if(!('cost' in dtl)) {
            dtl['cost']=0;
        }
        dtl.editable=dtl.status==0&&dtl.power=='O';
        this.ext=decodeExt(dtl.comment, tmpl);
        this.dtl=dtl;
    });
},
query_costs(pg) {
    var pgSize=this.service.N_SMPG;
    var offset=(parseInt(pg)-1)*pgSize;
    var url="/api/cost/list?customer="+this.dtl.customer+"&order="+this.id
            +"&offset="+offset+"&num="+pgSize;
    request({method:"GET",url:url}, this.service.name).then(resp=>{
        if(resp.code!=0||resp.data.total==0) {
            this.costs=[];
            this.cost.max=0;
            return;
        }
        var dt=new Date();
        var total=0;
        var opeartor=this.ibf.userInfo.account;
        //id,createAt,creator,cost,flowid,did
        this.costs=resp.data.list.map(l=>{ 
            dt.setTime(l.createAt*60000);
            l.createAt=datetime2str(dt);
            l.type=this.tags.cost.types[l.type];
            l.rmvAble=l.creator==opeartor&&l.flowid==0;//自己创建的才可以删除
            l.ext=decodeExt(l.cmt, this.cost.tmpl);
            total+=l.val;
            return l;
        });
        this.cost.max=Math.ceil(resp.data.total/pgSize);
        this.dtl.cost=total;
    });
},
query_payments(pg) {
    var pgSize=this.service.N_SMPG;
    var offset=(parseInt(pg)-1)*pgSize;
    var url="/api/payment/list?customer="+this.dtl.customer+"&order="+this.id+"&offset="+offset+"&num="+pgSize;
    request({method:"GET",url:url}, this.service.name).then(resp=>{
        if(resp.code != 0||resp.data.total==0) {
            return;
        }
        var dt=new Date();
        this.payments=resp.data.payments.map(l=>{
            dt.setTime(l.createAt*60000);
            l.createAt=datetime2str(dt);
            if(l.cfmAt<=0) {
                l.cfmAt=this.tags.payment.notCfm;
            } else {
                dt.setTime(l.cfmAt*60000);
                l.cfmAt=datetime2str(dt);
            }
            return l;
        })
        this.payment.max=Math.ceil(resp.data.total/pgSize);
    })
},
query_purchase() {
    var url="/api/order/purchaselist?order="+this.id;
    request({method:"GET",url:url}, this.service.name).then(resp=>{
        if(resp.code != 0||resp.data.total==0) {
            return;
        }
        //id,cost,expDate,flSta status,flowid,
        //applicant,receiver,descr,type,payState
        var dt=new Date();
        this.purList=resp.data.list.map(l=>{
            dt.setTime(l.expDate*60000);
            l.expDate=date2str(dt);
            l.icon=sta2icon(l.status);
            return l;
        })
    })
},
query_business() {
    var url="/api/order/busilist?order="+this.id;
    request({method:"GET",url:url}, this.service.name).then(resp=>{
        if(resp.code != 0||resp.data.total==0) {
            return;
        }
        //id,pid,flowid,flSta status,start,end,overAt,
        //prjName,expense,subsidy,dest,reason
        var dt=new Date();
        this.busiList=resp.data.list.map(l=>{
            if(l.overAt>0) {
                dt.setTime(l.overAt*60000);
                l.overAt=datetime2str(dt);
            } else {
                l.overAt=this.tags.notOver;
            }
            dt.setTime(l.start*60000);
            l.start=datetime2str(dt);
            dt.setTime(l.end*60000);
            l.end=datetime2str(dt);
            l.icon=sta2icon(l.status);
            return l;
        })
    })
},
save_base() {
    var dta=copyObj(this.dtl,['price']);
    dta['comment']=encodeExt(this.ext);
    dta.id=this.id;
    request({method:"POST",url:"/api/order/setInfo",data:dta}, this.service.name).then(resp=>{
        if(resp.code != 0) {
            this.$refs.errMsg.showErr(resp.code, resp.info);
            return;
        }
        this.editBase=false;
    })
},
more_costs() {
    this.cost.visible=!this.cost.visible;
    if(this.cost.visible && this.costs.length==0) {
        this.query_costs(1);
    }
},
more_payments() {
    this.payment.visible=!this.payment.visible;
    if(this.payment.visible && this.payments.length==0) {
        this.query_payments(1);
    }
},
more_purchase() {
    this.purchase.visible=!this.purchase.visible;
    if(this.purchase.visible && this.purList.length==0) {
        this.query_purchase();
    }
},
more_business() {
    this.business.visible=!this.business.visible;
    if(this.business.visible && this.busiList.length==0) {
        this.query_business();
    }
},
add_cost() {
    var dta={customer:this.dtl.customer, order:this.id,
         cost:this.newCost.cost, type:this.newCost.type};
    dta.comment=encodeExt(this.newCost.ext);
    request({method:"POST",url:"/api/cost/create",data:dta}, this.service.name).then(resp=>{
        if(resp.code != 0) {
            this.$refs.errMsg.showErr(resp.code, resp.info);
            return;
        }
        this.cost.dlg=false;
        this.newCost={cost:'',ext:[]};
        this.query_costs(1);
    })
},
remove_cost(id) {
    request({method:"DELETE",url:"/api/cost/remove?id="+id}, this.service.name).then(resp=>{
        if(resp.code != 0) {
            this.$refs.errMsg.showErr(resp.code, resp.info);
            return;
        }
        this.query_costs(1);
    })
},
add_payment() {
    var dta=copyObj(this.newPayment, ["amount","bank"]);
    dta.order=this.id;
    dta.comment=encodeExt(this.newPayment.ext);
    request({method:"POST",url:"/api/payment/create",data:dta}, this.service.name).then(resp=>{
        if(resp.code != RetCode.OK) {
            this.$refs.errMsg.showErr(resp.code, resp.info);
            return;
        }
        this.payment.dlg=false;
        this.newPayment={amount:0,ext:[]};
        this.query_payments(1);
    })
},
order_flow(){
    var url='/workflow?flName=order&flow='+this.dtl.flowid
        +"&did="+this.id+"&dtlApi="+encodeURIComponent("/order/detail");
    this.service.goto(url);
},
menu_remove(){
    var msg=this.tags.cfmToDel+this.tags.order.title+' "'+this.dtl.cname+'-'+this.dtl.skuName+'"';
    this.$refs.confirmDlg.show(msg, ()=>{
        var opts={method:"DELETE",url:"/api/order/remove?id="+this.id};
        request(opts, this.service.name).then(resp=>{
            if(resp.code != 0) {
                this.$refs.errMsg.showErr(resp.code, resp.info);
            }else{
                this.service.go_back();
            }
        })
    })
},
open_new_payment() {
    var defaultVal={cmt:{n:this.tags.cmt,t:'s'}};
    var url="/api/proxy/gettemplate?name=payment";
    this.ibf.template('payment', url, defaultVal).then(tmpl=> {
        //{a:{n:xxx,t:s/d/n},b:{}}
        this.newPayment.amount='';
        this.newPayment.bank='';
        this.newPayment.ext=decodeExt('{}',tmpl);
        this.payment.dlg=true
    })
},
open_new_cost() {
    //{a:{n:xxx,t:s/d/n},b:{}}
    this.newCost.cost='';
    this.newCost.type='';
    this.newCost.ext=decodeExt('{}',this.cost.tmpl);
    this.cost.dlg=true
},
show_purchase() {
    copyObjTo(EMPTY_PUR, this.purchase.dta);
    this.userInput={uid:0,account:''};
    this.purchase.skus=[];
    this.purchase.sku={sku:{id:0,name:''},num:''};
    this.purchase.dlg=true;
},
purchase_do() {
    var pur=this.purchase.dta;
    var dta=copyObj(pur, ['receiver','descr','type']);
    dta.order=this.id;
    dta.expDate=parseInt(Date.parse(pur.expDate)/60000);
    dta.buyer=this.userInput.account;
    dta.skus=this.purchase.skus;
    request({method:"POST", url:"/order/purchase", data:dta}, this.service.name).then(resp=>{
        if(resp.code != RetCode.OK) {
            this.$refs.errMsg.showErr(resp.code, resp.info);
            return;
        }
        this.purchase.dlg=false;
        this.query_purList();
    })
},
add_purchase_sku() {
    var sku=this.purchase.sku.sku;
    var num=this.purchase.sku.num;
    if(sku.id==0 || !num)return;
    this.purchase.skus.push({sku:sku.id,skuName:sku.name,num:num});
    this.purchase.sku.sku={id:0,name:''};
    this.purchase.sku.num='';
},
rmv_purchase_sku(i){
    this.purchase.skus.splice(i,1);
},
show_busi() {
    copyObjTo(EMPTY_BUSI, this.business.dta);
    this.userInput={uid:0,account:''};
    this.business.dlg=true;
},
busi_do() {
    var busi=this.business;
    var dta=copyObj(busi.dta, ['cmt','reason','dest']);
    dta.order=this.id;
    dta.uid=this.userInput.id;
    dta.account=this.userInput.account;
    dta.start=parseInt(Date.parse(busi.dta.start)/60000);
    dta.end=parseInt(Date.parse(busi.dta.end)/60000);

    request({method:"POST", url:"/order/business", data:dta}, this.service.name).then(resp=>{
        if(resp.code != RetCode.OK) {
            this.$refs.errMsg.showErr(resp.code, resp.info);
            return;
        }
        this.business.dlg=false;
        this.query_busiList();
    })
},
show_workflow(flowid, did) {
    _WF_.showPage(flowid, did, this.$router);
}
},
template:`
<q-layout view="hHh lpr fFf">
  <q-header>
    <q-toolbar>
      <q-btn flat round icon="arrow_back" dense @click="service.back"></q-btn>
      <q-toolbar-title>{{dtl.cname}}-{{dtl.prjName}}</q-toolbar-title>
      <q-btn flat round dense icon="menu" v-if="dtl.editable">
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
  <template v-slot:action v-if="dtl.editable">
    <q-icon name="edit" color="primary" @click.stop="editBase=true"></q-icon>
  </template>
</q-banner>
<q-list dense>
  <q-item clickable @click.stop="service.goto('/customer?id='+dtl.customer)">
    <q-item-section>{{tags.order.cname}}</q-item-section>
    <q-item-section><span class="text-primary">{{dtl.cname}}</span></q-item-section>
  </q-item>
  <q-item v-for="i in visSegs">
    <q-item-section>{{tags.order[i]}}</q-item-section>
    <q-item-section>{{dtl[i]}}</q-item-section>
  </q-item>
  <q-item clickable @click.stop="order_flow">
    <q-item-section>{{tags.order.status}}</q-item-section>
    <q-item-section><q-icon :name="dtl.icon" color="blue"></q-icon></q-item-section>
  </q-item>
  <q-item v-for="e in ext">
    <q-item-section>{{e.n}}</q-item-section>
    <q-item-section>{{e.v}}</q-item-section>
  </q-item>
  <q-item clickable @click.stop="service.goto('/ibf/prjproc?id='+dtl.pid)">
    <q-item-section>{{tags.order.prj}}</q-item-section>
    <q-item-section class="text-blue">{{dtl.prjName}}</q-item-section>
  </q-item>
</q-list>

<!-- 销售清单 -->
<q-banner dense inline-actions class="q-mb-sm text-dark bg-blue-grey-1">
{{tags.order.skuList}}
</q-banner>
<q-list dense separator>
 <q-item v-for="l in dtl.skus">
  <q-item-section>{{l.skuName}}</q-item-section>
  <q-item-section>{{l.num}}/{{l.sent}}</q-item-section>
  <q-item-section side>{{l.price}}</q-item-section>
 </q-item>
</q-list>

<!-- 采购记录 -->
<q-banner dense inline-actions class="q-mb-sm text-dark bg-blue-grey-1" @click="more_purchase">
 <template v-slot:avatar>
  <q-icon name="shopping_cart" color="primary" size="1em"></q-icon>
 </template>
 {{tags.purchase.title}}
 <template v-slot:action>
  <q-icon name="add_circle" color="primary" @click.stop="show_purchase"></q-icon>
 </template>
</q-banner>
<q-list separator dense v-show="purchase.visible">
 <q-item v-for="p in purList" clickable @click="show_workflow(p.flowid,p.id)">
  <q-item-section>
   <q-item-label>{{p.applicant}}</q-item-label>
   <q-item-label caption>{{p.cost}}</q-item-label>
  </q-item-section>
  <q-item-section>
   <q-item-label>{{p.receiver}}</q-item-label>
   <q-item-label caption>{{p.expDate}}</q-item-label>
  </q-item-section>
  <q-item-section>{{p.descr}}</q-item-section>
  <q-item-section side>
   <q-icon :name="p.icon" color="blue"></q-icon>
  </q-item-section>
 </q-item>
</q-list>

<!-- 差旅记录 -->
<q-banner dense inline-actions class="q-mb-sm text-dark bg-blue-grey-1" @click="more_business">
 <template v-slot:avatar>
  <q-icon name="flight_takeoff" color="primary" size="1em"></q-icon>
 </template>
 {{tags.busi.title}}
 <template v-slot:action>
  <q-icon name="add_circle" color="primary" @click.stop="show_busi"></q-icon>
 </template>
</q-banner>
<q-list separator dense v-show="business.visible">
 <q-item v-for="b in busiList" clickable @click="show_workflow(b.flowid,b.id)">
  <q-item-section>
   <q-item-label>{{b.account}}</q-item-label>
   <q-item-label caption>{{b.start}}</q-item-label>
   <q-item-label caption>{{b.end}}</q-item-label>
  </q-item-section>
  <q-item-section>
   <q-item-label>{{b.overAt}}</q-item-label>
   <q-item-label caption>{{b.subsidy}}</q-item-label>
   <q-item-label caption>{{b.expense}}</q-item-label>
  </q-item-section>
  <q-item-section>
   <q-item-label>{{b.dest}}</q-item-label>
   <q-item-label caption>{{b.reason}}</q-item-label>
  </q-item-section>
  <q-item-section side>
   <q-icon :name="b.icon" color="blue"></q-icon>
  </q-item-section>
 </q-item>
</q-list>

<!-- 成本记录 -->
<q-banner dense inline-actions class="q-mb-sm text-dark bg-blue-grey-1" @click="more_costs">
 <template v-slot:avatar>
  <q-icon :name="tags.icons.service" color="primary" size="1em"></q-icon>
 </template>
 {{tags.cost.title}}:{{dtl.cost}}
 <template v-slot:action>
  <q-icon name="add_circle" color="primary" @click.stop="open_new_cost"></q-icon>
 </template>
</q-banner>
<div v-show="cost.visible">
<q-list separator dense>
 <q-item v-for="s in costs">
  <q-item-section>
   <q-item-label>{{s.creator}}</q-item-label>
   <q-item-label caption>{{s.createAt}}</q-item-label>
  </q-item-section>
  <q-item-section>
   <q-item-label>{{s.type}}:{{s.val}}</q-item-label>
   <q-item-label v-for="e in s.ext" caption>
     {{e.n}}:{{e.v}}
   </q-item-label>
  </q-item-section>
  <q-item-section thumbnail>
   <q-icon name="cancel" color="red" @click="remove_cost(s.id)" v-if="s.rmvAble"></q-icon>
   <q-icon name="star" color="primary" @click="show_workflow(s.flowid,s.did)" v-if="s.flowid>0"></q-icon>
  </q-item-section>
 </q-item>
</q-list>
<div class="q-pa-sm flex flex-center" v-if="cost.max>1">
 <q-pagination color="primary" :max="cost.max" max-pages="10" v-model="cost.cur"
 dense boundary-numbers="false" @update:model-value="query_costs"></q-pagination>
</div>
</div>

<!-- 回款列表 -->
<q-banner dense inline-actions class="q-mb-sm text-dark bg-blue-grey-1" @click="more_payments">
 <template v-slot:avatar>
  <q-icon :name="tags.icons.payment" color="primary" size="1em"></q-icon>
 </template>
 {{tags.payment.title}}({{tags.order.payment}}:{{dtl.payment}},{{tags.order.needPay}}:{{dtl.needPay}})
 <template v-slot:action>
  <q-icon name="add_circle" color="primary" @click.stop="open_new_payment"></q-icon>
 </template>
</q-banner>
<div v-show="payment.visible">
<q-list separator dense>
 <q-item v-for="p in payments">
  <q-item-section>
   <q-item-label>{{p.creator}}</q-item-label>
   <q-item-label caption>{{p.createAt}}</q-item-label>
  </q-item-section>
  <q-item-section>{{p.amount}}</q-item-section>
  <q-item-section>{{p.cfmAt}}</q-item-section>
 </q-item>
</q-list>
<div class="q-pa-sm flex flex-center" v-if="payment.max>1">
 <q-pagination color="primary" :max="payment.max" max-pages="10" v-model="payment.cur"
 dense boundary-numbers="false" @update:model-value="query_payments"></q-pagination>
</div>
</div>
    </q-page>
  </q-page-container>
</q-layout>

<component-alert-dialog :title="tags.failToCall" :errMsgs="tags.errMsgs" ref="errMsg"></component-alert-dialog>
<component-confirm-dialog :title="tags.alert" :close="tags.cancel" :ok="tags.ok" ref="confirmDlg"></component-confirm-dialog>

<!-- 新增成本弹窗 -->
<q-dialog v-model="cost.dlg" no-backdrop-dismiss>
  <q-card style="min-width:70vw">
    <q-card-section>
      <div class="text-h6">{{tags.cost.title}}</div>
    </q-card-section>
    <q-card-section class="q-pt-none">
    <q-list>
      <q-item><q-item-section>
       <q-select v-model="newCost.type" :options="cost.tpOpts" emit-value
        :label="tags.cost.type" dense map-options></q-select>
      </q-item-section></q-item>
      <q-item><q-item-section>
        <q-input :label="tags.cost.val" v-model.number="newCost.cost" dense type="number"></q-input>
      </q-item-section></q-item>
      <!-- ext/comment -->
      <q-item v-for="e in newCost.ext"><q-item-section>
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
      <q-btn :label="tags.ok" color="primary" @click="add_cost"></q-btn>
      <q-btn flat :label="tags.close" color="primary" v-close-popup></q-btn>
    </q-card-actions>
  </q-card>
</q-dialog>

<!-- 新增回款弹窗 -->
<q-dialog v-model="payment.dlg" no-backdrop-dismiss>
  <q-card style="min-width:70vw">
    <q-card-section>
      <div class="text-h6">{{tags.payment.title}}</div>
    </q-card-section>
    <q-card-section class="q-pt-none">
    <q-list>
      <q-item><q-item-section>
       <bank-select :label="tags.payment.bank" v-model="newPayment.bank" dense></bank-select>
      </q-item-section></q-item>
      <q-item><q-item-section>
       <q-input :label="tags.payment.amount" v-model="newPayment.amount" type="number" dense></q-input>
      </q-item-section></q-item>
      <!-- ext/comment -->
      <q-item v-for="e in newPayment.ext"><q-item-section>
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
      <q-btn :label="tags.ok" color="primary" @click="add_payment"></q-btn>
      <q-btn flat :label="tags.close" color="primary" v-close-popup></q-btn>
    </q-card-actions>
  </q-card>
</q-dialog>

<!-- 修改订单基本信息弹窗 -->
<q-dialog v-model="editBase" no-backdrop-dismiss>
  <q-card style="min-width:70vw">
    <q-card-section>
      <div class="text-h6">{{tags.baseInfo}}</div>
    </q-card-section>
    <q-card-section class="q-pt-none">
    <q-list dense>
      <q-item><q-item-section>{{dtl.cname}}</q-item-section></q-item>
      <q-item><q-item-section>
        <q-input :label="tags.order.price" v-model="dtl.price" dense></q-input>
      </q-item-section></q-item>
      <q-item v-for="e in ext"><q-item-section>
        <div v-if="e.t=='d'">
          <component-date-input :close="tags.ok" :label="e.k" v-model="e.v"></component-date-input>
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

<!-- 新建采购单 -->
<q-dialog v-model="purchase.dlg">
<q-card style="min-width:70vw">
 <q-card-section>
  <div class="text-h6">{{tags.purchase.title}}</div>
 </q-card-section>
 <q-card-section class="q-pt-none">
  <q-input v-model="purchase.dta.receiver" dense :label="tags.purchase.receiver"></q-input>
  <component-date-input v-model="purchase.dta.expDate" :format="tags.dateFmt"
  :label="tags.purchase.expDate" min="today"></component-date-input>
  <user-input v-model="userInput" :label="tags.purchase.buyer"></user-input>
  <q-input v-model="purchase.dta.descr" :label="tags.cmt" dense></q-input>
  <q-banner inline-actions class="bg-indigo-1 q-mt-sm" dense>
    {{tags.purchase.skuList}}
  </q-banner>
  <q-list>
   <q-item clickable v-for="(s,i) in purchase.skus">
    <q-item-section>{{s.skuName}}</q-item-section>
    <q-item-section>{{s.num}}</q-item-section>
    <q-item-section side>
     <q-icon color="red" name="clear" @click="rmv_purchase_sku(i)"></q-icon>
    </q-item-section>
   </q-item>
   <q-item>
    <q-item-section>
     <component-sku-selector v-model="purchase.sku.sku"
      :label="tags.purchase.sku"></component-sku-selector>
    </q-item-section>
    <q-item-section>
     <q-input v-model.number="purchase.sku.num" :label="tags.order.skuNum" dense type="number"></q-input>
    </q-item-section>
    <q-item-section side>
     <q-icon name="add_circle" @click="add_purchase_sku" color="primary"></q-icon>
    </q-item-section>
   </q-item>
  </q-list>
 </q-card-section>
 <q-card-actions align="right">
   <q-btn flat :label="tags.close" color="primary" v-close-popup></q-btn>
   <q-btn :label="tags.ok" color="primary" @click="purchase_do"></q-btn>
 </q-card-actions>
</q-card>
</q-dialog>

<!-- 新建差旅 -->
<q-dialog v-model="business.dlg">
 <q-card style="min-width:70vw">
  <q-card-section>
   <div class="text-h6">{{tags.add}} {{tags.busi.title}}</div>
  </q-card-section>
  <q-card-section class="q-pt-none">
   <user-input v-model="userInput" :label="tags.busi.account"></user-input>
   <component-date-input v-model="business.dta.start" :label="tags.start"
    :format="tags.dateFmt"></component-date-input>
   <component-date-input v-model="business.dta.end" :label="tags.end"
    :format="tags.dateFmt" min="today"></component-date-input>
   <q-input v-model="business.dta.dest" :label="tags.busi.dest"></q-input>
   <q-input v-model="business.dta.reason" :label="tags.busi.reason"></q-input>
   <q-input v-model="business.dta.cmt" :label="tags.cmt" type="textarea" rows="2"></q-input>
  </q-card-section>
  <q-card-actions align="right">
    <q-btn flat :label="tags.close" color="primary" v-close-popup></q-btn>
    <q-btn :label="tags.ok" color="primary" @click="busi_do"></q-btn>
  </q-card-actions>
 </q-card>
</q-dialog>
`
}
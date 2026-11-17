import {sta2icon} from '/assets/v3/components/workflow.js';
import {encodeExt,decodeExt} from '/assets/v3/settings/config.js';

export default {
inject:['service', 'tags', "ibf"],
data() {return {
    customers:[], //客户列表
    ctrl:{cur:1, max:0,search:'',onlyMine:true},
    newCust:{name:'',taxid:'',address:'',business:'',nextSigners:[],ext:{},dlg:false}
}},
created(){
    this.ctrl.cur=this.ibf.getRt("cur",1);
    this.ctrl.onlyMine=this.ibf.getRt("onlyMine",'false') == 'true';
    this.query(this.ctrl.cur);
},
methods:{
fmt_lines(data) {
    var dt=new Date();
    var rows=data.touchlogs;
    var touchlogs=rows?rows:{};//可能无联系记录

    var customers=[];
    var cu,tl;
    var cols=data.cols;
    rows=data.customers;
    for(var row of rows) { //id,name,address,createAt,status,creator
        cu={};
        for(var i in cols) {
            cu[cols[i]]=row[i];
        }
        dt.setTime(cu.createAt*60000);
        cu.createAt=date2str(dt);
        cu.status=sta2icon(cu.status);
        tl=touchlogs[cu.id];//客户可以没有最新的接触记录
        if(tl) {//customer->cmt,createAt,creator,contact
            cu['comment']=tl[0]+'@'+tl[3];
            dt.setTime(tl[1]*60000);
            cu['tlCreator']=tl[2]+'@'+date2str(dt);
        }
        customers.push(cu);
    }
    this.customers=customers;
},
query(pg) {
    this.ibf.setRt("cur", pg);
    this.ctrl.search='';
    var offset=(parseInt(pg)-1)*this.service.N_PAGE;
    var url = this.ctrl.onlyMine ? "/api/customer/my" : "/api/customer/readable";
    url += "?offset="+offset+"&num="+this.service.N_PAGE;
    request({method:"GET",url:url}, this.service.name).then(resp =>{
        if(resp.code!=RetCode.OK || resp.data.total==0) {
            this.customers=[];
            this.ctrl.max=0;
            this.ctrl.cur=1;
            return;
        }
        this.fmt_lines(resp.data);
        this.ctrl.max=Math.ceil(resp.data.total/this.service.N_PAGE);
    })
},
search() {
    if(this.ctrl.search=='') {
        this.query(1);
        return;
    }
    var url="/api/customer/search?s="+this.ctrl.search+"&limit="+this.service.N_PAGE;
    request({method:"GET",url:url}, this.service.name).then(resp => {
        if(resp.code != RetCode.OK) {
            return;
        }
        this.fmt_lines(resp.data);
        this.ctrl.max=1;
    })
},
onlyMineClk() {
    this.ibf.setRt("onlyMine",this.ctrl.onlyMine);
    this.ctrl.cur=1;
    this.query(1);
},
create() {
    var dta=copyObj(this.newCust,['name','taxid','address','business','nextSigners']);
    dta.comment=encodeExt(this.newCust.ext);
    var url="/api/customer/create";
    request({method:"POST",url:url,data:dta}, this.service.name).then(resp => {
        if(resp.code != 0) {
            this.$refs.errMsg.showErr(resp.code, resp.info);
            return;
        }
        this.newCust.dlg=false;
        this.newCust={name:'',taxid:'',address:'',business:'',nextSigners:[],ext:{}};
        this.query(1);
    })
},
chkCredit(code) {//不能在rules中直接调用原生对象的函数，原因未知
    return JStr.chkCreditCode(code);
},
show_create() {
    var defaultVal={cmt:{n:this.tags.cmt,t:'s'}};
    var url="/api/proxy/gettemplate?name=customer";
    this.ibf.template('customer', url, defaultVal).then(tmpl=>{//{k:"x",n:"y",t:"z"}..
        this.newCust.ext=decodeExt("{}", tmpl);
        this.newCust.dlg=true
    });
}
},
template:`
<q-layout view="hHh lpr fFf">
  <q-header>
   <q-toolbar>
    <q-btn flat round icon="arrow_back" dense @click="service.back"></q-btn>
    <q-toolbar-title>{{tags.home.customers}}</q-toolbar-title>
    <q-btn flat round dense icon="menu">
      <q-menu>
       <q-list style="min-width: 100px">
        <q-item clickable v-close-popup>
          <q-item-section avatar>
           <q-checkbox v-model="ctrl.onlyMine" @update:model-value="onlyMineClk"></q-checkbox>
          </q-item-section>
          <q-item-section>{{tags.onlyMine}}</q-item-section>
        </q-item>
       </q-list>
      </q-menu>
    </q-btn>
  </q-toolbar>
  </q-header>
  <q-footer class="bg-white q-pa-md">
    <q-input outlined v-model="ctrl.search" :label="tags.search" dense @keyup.enter="search">
     <template v-slot:append>
      <q-icon v-if="ctrl.search!==''" name="close" @click="query(1)" class="cursor-pointer"></q-icon>
      <q-icon name="search" @click="search"></q-icon>
     </template>
     <template v-slot:after>
      <q-btn round color="primary" icon="add_circle" @click="show_create"></q-btn>
     </template>
    </q-input>
  </q-footer>
  <q-page-container>
    <q-page class="q-pa-md">
<div class="q-pa-sm flex flex-center" v-if="ctrl.max>1">
 <q-pagination v-model="ctrl.cur" color="primary" :max="ctrl.max" max-pages="10"
  boundary-numbers="false" @update:model-value="query"></q-pagination>
</div>
<q-list separator>
 <q-item>
  <q-item-section><q-item-label caption>{{tags.customer.name}}</q-item-label></q-item-section>
  <q-item-section><q-item-label caption>{{tags.customer.address}}</q-item-label></q-item-section>
  <q-item-section><q-item-label caption>{{tags.customer.lastestTl}}</q-item-label></q-item-section>
  <q-item-section thumbnail></q-item-section>
 </q-item>
 <q-item v-for="c in customers" @click="service.goto('/customer?id='+c.id)" clickable>
  <q-item-section>
   <q-item-label>{{c.name}}</q-item-label>
   <q-item-label caption>{{c.creator}}@{{c.createAt}}</q-item-label>
  </q-item-section>
  <q-item-section>{{c.address}}</q-item-section>
  <q-item-section no-wrap>
   <q-item-label caption lines=2>{{c.comment}}</q-item-label>
   <q-item-label caption>{{c.tlCreator}}</q-item-label>
  </q-item-section>
  <q-item-section thumbnail><q-icon :name="c.status" color="primary" size="xs"></q-icon></q-item-section>
 </q-item>
</q-list>
    </q-page>
  </q-page-container>
</q-layout>
<component-alert-dialog :title="tags.failToCall" :errMsgs="tags.errMsgs" ref="errMsg"></component-alert-dialog>

<q-dialog v-model="newCust.dlg">
  <q-card style="min-width:70vw">
    <q-card-section>
      <div class="text-h6">{{tags.addCust}}</div>
    </q-card-section>
    <q-card-section class="q-pt-none">
     <q-list>
      <q-item><q-item-section>
       <q-input v-model="newCust.name" :label="tags.customer.name" dense maxlength=100></q-input>
      </q-item-section></q-item>
      <q-item><q-item-section>
       <q-input v-model="newCust.taxid" :label="tags.taxid" dense maxlength=18
       :rules="[v=>chkCredit(v)||tags.taxidPls]"></q-input>
      </q-item-section></q-item>
      <q-item><q-item-section>
       <q-input v-model="newCust.address" :label="tags.address" dense maxlength=100></q-input>
      </q-item-section></q-item>
      <q-item><q-item-section>
       <q-input v-model="newCust.business" :label="tags.business" dense maxlength=100></q-input>
      </q-item-section></q-item>
      <q-item v-for="e in newCust.ext"><q-item-section>
        <div v-if="e.t=='d'">
          <component-date-input :close="tags.ok" :label="e.n" v-model="e.v" dense></component-date-input>
        </div>
        <div v-else-if="e.t=='b'">
          <q-checkbox v-model="e.v" :label="e.n" left-label dense></q-checkbox>
        </div>
        <div v-else>
         <q-input :label="e.n" v-model="e.v" dense :autogrow="e.t!='n'"
          :type="e.t=='n'?'number':'textarea'" dense></q-input>
        </div>
      </q-item-section></q-item>
      <q-item><q-item-section>
       <component-user-selector :label="tags.signers" :accounts="newCust.nextSigners"></component-user-selector>
      </q-item-section></q-item>
     </q-list>
    </q-card-section>
    <q-card-actions align="right">
      <q-btn :label="tags.ok" color="primary" @click="create"></q-btn>
      <q-btn flat :label="tags.close" color="primary" v-close-popup></q-btn>
    </q-card-actions>
  </q-card>
</q-dialog>
`
}
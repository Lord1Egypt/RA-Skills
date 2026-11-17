export default {
inject:['service', 'tags'],
data() {return {
    list:[], //采购单
    ctrl:{cur:1,max:0,search:''}
}},
created(){
    this.query(1)
},
methods:{
query(pg) {
    var offset=(parseInt(pg)-1)*this.service.N_PAGE;
    var opts={method:"GET", url:"/purchase/list?num="+this.service.N_PAGE+"&offset="+offset}
    request(opts, this.service.name).then(resp => {
        if(resp.code!=RetCode.OK) {
            this.list=[];
            this.ctrl.max=0;
            this.ctrl.cur=1;
            return;
        }
        this.list=this.fmt_lines(resp.data);
        this.ctrl.max=Math.ceil(resp.data.total/this.service.N_PAGE);
    })
},
search() {
    if(this.ctrl.search=='') {
        this.query(1);
        return;
    }
    var url="/purchase/search?s="+this.ctrl.search+"&limit="+this.service.N_PAGE;
    request({method:"GET",url:url}, this.service.name).then(resp => {
        if(resp.code != RetCode.OK) {
            return;
        }
        this.list=this.fmt_lines(resp.data);
        this.ctrl.max=1;
    })
},
fmt_lines(data) {
    var dt=new Date();
    var cols=data.cols;
    var types=this.tags.purType;
    var states=this.tags.purState;
    var l,ll=[];
    //id,cost,pid,prjName,expDate,flSta status,flowid,
    //applicant,receiver,descr,type
    for(var row of data.list) { 
        l={};
        for(var i in cols) {
           l[cols[i]]=row[i];
        }
        dt.setTime(l.expDate*60000);
        l.expDate=datetime2str(dt);
        l.type=types[l.type];
        l.color=l.state=='OVER'?'':'text-primary';
        l.state=states[l.state];
        ll.push(l);
    }
    return ll;
}
},
template:`
<q-layout view="hHh lpr fFf">
  <q-header>
   <q-toolbar>
     <q-btn flat icon="arrow_back" dense @click="service.back()"></q-btn>
     <q-toolbar-title>{{tags.purchase.title}}</q-toolbar-title>
   </q-toolbar>
  </q-header>
  <q-footer class="bg-white q-pa-md">
    <q-input outlined v-model="ctrl.search" :label="tags.search" dense @keyup.enter="search">
     <template v-slot:append>
      <q-icon v-if="ctrl.search!==''" name="close" @click="query(1)" class="cursor-pointer"></q-icon>
      <q-icon name="search" @click="search"></q-icon>
     </template>
    </q-input>
  </q-footer>
  <q-page-container>
    <q-page class="q-pa-sm">
 <q-list dense separator>
  <q-item>
   <q-item-section><q-item-label caption>{{tags.prjName}}</q-item-label></q-item-section>
   <q-item-section><q-item-label caption>{{tags.purchase.cost}}</q-item-label></q-item-section>
   <q-item-section><q-item-label caption>{{tags.receiver}}</q-item-label></q-item-section>
   <q-item-section side><q-item-label caption>{{tags.expDate}}</q-item-label></q-item-section>
  </q-item>
  <q-item v-for="(l,i) in list" clickable
   @click="service.goto('/purchasedtl?id='+l.id)">
    <q-item-section>
     <q-item-label :class="l.color">{{l.prjName}}</q-item-label>
     <q-item-label caption>{{l.type}}/{{l.state}}</q-item-label>
    </q-item-section>
    <q-item-section>{{l.cost}}</q-item-section>
    <q-item-section>
     <q-item-label>{{l.receiver}}</q-item-label>
     <q-item-label caption>{{l.descr}}</q-item-label>
    </q-item-section>
    <q-item-section side>
     <q-item-label>{{l.expDate}}</q-item-label>
     <q-item-label caption>{{l.applicant}}</q-item-label>
    </q-item-section>
  </q-item>
 </q-list>
    </q-page>
  </q-page-container>
</q-layout>
`
}